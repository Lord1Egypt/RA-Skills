const EMPTY_PRJ={name:'',cmt:'',scope:'',start:'',end:'',type:'',owner:[],leader:[]};
export default {
inject:['service', 'ibf'],
data() {return {
    list:[], //项目列表
    search:'',
    tags:this.ibf.tags,
    ctrl:{cur:1, max:0,prjDlg:false},
    prj:{},
    typeOpts:[]
}},
created(){
    this.ctrl.cur=this.ibf.getRt("cur",1);
    this.query(this.ctrl.cur);
    for(var i in this.tags.prj.typeCfg) {
        this.typeOpts.push({label:this.tags.prj.typeCfg[i],value:i});
    }
    copyObjTo(EMPTY_PRJ, this.prj);
},
methods:{
fmt_lines(data) {
    var dt=new Date();
    var list=[];
    var p; //项目
    var cols=data.cols;
    var rows=data.list;
    var stage;
    //id,fid,name,start,end,stage
    for(var row of rows) {
        p={};
        for(var i in cols) {
            p[cols[i]]=row[i];
        }
        dt.setTime(p.start*60000);
        p.start_s=date2str(dt);
        dt.setTime(p.end*60000);
        p.end_s=date2str(dt);
        p.type_s=this.tags.prj.typeCfg[p.type];
        stage=this.tags.prj.stageCfg[p.stage];
        p.stage_s=stage?stage:p.stage;//有自定义的状态名称
        list.push(p);
    }
    this.list=list;
},
query(pg) {
    this.ibf.setRt("cur",pg);
    this.search='';
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var url = "/api/project/list?offset="+offset+"&num="+this.service.N_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp =>{
        if(resp.code!=RetCode.OK || resp.data.total==0) {
            this.list=[];
            this.ctrl.max=0;
            this.ctrl.cur=1;
            return;
        }
        this.fmt_lines(resp.data);
        this.ctrl.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},
doSearch() {
    if(this.search=='') {
        this.query(this.ctrl.cur);
        return;
    }
    var url="/api/project/search?s="+this.search+"&limit="+this.service.N_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            return;
        }
        this.fmt_lines(resp.data);
        this.ctrl.cur=1;
        this.ctrl.max=1;
    })
},
add_prj() {
    this.prj.start=parseInt(new Date(this.prj.start_s).getTime()/60000);
    this.prj.end=parseInt(new Date(this.prj.end_s).getTime()/60000);
    var dta=copyObj(this.prj, dta, ['name','cmt','scope','type','start','end']);
    dta.owner=this.prj.owner[0];
    dta.leader=this.prj.leader[0];
    var opts={method:"POST",url:"/project/create",data:dta};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.query(this.ctrl.cur);
        this.ctrl.prjDlg=false;
        copyObjTo(EMPTY_PRJ, this.prj);
    });
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat icon="arrow_back" dense @click="service.back"></q-btn>
    <q-toolbar-title>{{tags.prj.title}}</q-toolbar-title>
    <q-btn icon="add_circle" @click="ctrl.prjDlg=true" flat></q-btn>
  </q-toolbar>
  </q-header>
  <q-footer class="bg-white q-pa-md">
    <q-input outlined v-model="search" :label="tags.search" dense @keyup.enter="doSearch">
     <template v-slot:append>
      <q-icon v-if="search!==''" name="close" @click="query(1)" class="cursor-pointer"></q-icon>
      <q-icon name="search" @click="doSearch"></q-icon>
     </template>
    </q-input>
  </q-footer>
  <q-page-container>
    <q-page class="q-pa-md">
<div class="q-pa-md flex flex-center" v-show="ctrl.max>1">
 <q-pagination v-model="ctrl.cur" color="primary" :max="ctrl.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query"></q-pagination>
</div>
<q-list separator>
 <q-item v-for="p in list" clickable @click="ibf.goto('/project?id='+p.id)">
  <q-item-section>
   <q-item-label>{{p.name}}({{p.type_s}})</q-item-label>
   <q-item-label caption>{{p.start_s}}--{{p.end_s}}</q-item-label>
  </q-item-section>
  <q-item-section>
   <q-item-label>{{p.stage_s}}</q-item-label>
   <q-item-label caption>{{p.scope}}</q-item-label>
  </q-item-section>
  <q-item-section>
   <q-item-label>{{p.cmt}}</q-item-label>
  </q-item-section>
 </q-item>
</q-list>
  </q-page>
 </q-page-container>
</q-layout>

<q-dialog v-model="ctrl.prjDlg">
 <q-card style="min-width:70vw">
  <q-card-section>
    <div class="text-h6">{{tags.add}} {{tags.prj.title}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-input :label="tags.name" v-model="prj.name" dense></q-input>
   <q-select :label="tags.prj.type" v-model="prj.type" :options="typeOpts"
    dense map-options emit-value></q-select>
   <date-input :close="tags.ok" :label="tags.prj.start" v-model="prj.start_s"></date-input>
   <date-input :close="tags.ok" :label="tags.prj.end" v-model="prj.end_s" min="today"></date-input>
   <user-selector :label="tags.prj.owner" :accounts="prj.owner" :multi="false"></user-selector>
   <user-selector :label="tags.prj.leader" :accounts="prj.leader" :multi="false"></user-selector>
   <q-input :label="tags.cmt" v-model="prj.cmt" dense></q-input>
   <q-input :label="tags.prj.scope" v-model="prj.scope" dense type="textarea" rows="2"></q-input>
  </q-card-section>
  <q-card-actions align="right">
   <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
   <q-btn :label="tags.ok" color="primary" @click="add_prj"></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
`
}