import AlertDialog from "/assets/v3/components/alert_dialog.js"
import DateInput from "/assets/v3/components/date_input.js"

const EMPTY_RI={start_s:'',end_s:'',org:'',type:'',contrib:'',cmt:''};
export default {
components:{
    "alert-dialog":AlertDialog,
    "date-input":DateInput
},
inject:['ibf'],
data() {return {
    uid:this.$route.query.uid,
    list:[],
    tags:this.ibf.tags,
    rsInfo:{uid:this.$route.query.uid},
    ctrl:{act:'',dlg:false,tag:''},
    opts:{type:[]}
}},
created(){
    this.query();
    var opts=[];
    for(var i in this.tags.resume.types) {
        opts.push({value:i, label:this.tags.resume.types[i]});
    }
    this.opts.type=opts;
},
methods:{
query() {
    var url = "/api/resume/list?uid="+this.uid;
    request({method:"GET",url:url}, this.ibf.SERVICE_HR).then(resp =>{
        if(resp.code!=RetCode.OK) {
            return;
        }
        var ll=[];
        var dt=new Date();
        for(var l of resp.data.list) {
            dt.setTime(l.start*60000);
            l.start_s=date2str(dt);
            dt.setTime(l.end*60000);
            l.end_s=date2str(dt);
            l.type_s=this.tags.resume.types[l.type];
            ll.push(l);
        }
        this.list=ll;
    })
},
add() {
    var dta=copyObjExc(this.rsInfo,['start','end','start_s', 'end_s']);
    dta.start=parseInt(new Date(this.rsInfo.start_s).getTime()/60000);
    dta.end=parseInt(new Date(this.rsInfo.end_s).getTime()/60000);
    request({method:"POST",url:"/api/resume/add",data:dta}, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.ctrl.dlg=false;
        this.query();
    });
},
update() {
    var dta=copyObjExc(this.rsInfo,['start','end','start_s', 'end_s']);
    dta.start=parseInt(new Date(this.rsInfo.start_s).getTime()/60000);
    dta.end=parseInt(new Date(this.rsInfo.end_s).getTime()/60000);
    request({method:"PUT",url:"/api/resume/update",data:dta}, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.ctrl.dlg=false;
        this.query();
    });
},
remove(start) {
    var url="/api/resume/remove?uid="+this.uid+"&start="+start;
    request({method:"DELETE",url:url}, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.ctrl.dlg=false;
        this.query();
    });
},
showAct(act,i) {
    if(act=='add') {
        this.ctrl.tag=this.tags.add;
        copyObjTo(EMPTY_RI,this.rsInfo);
    } else {
        this.ctrl.tag=this.tags.modify;
        copyObjTo(this.list[i],this.rsInfo);
    }
    this.ctrl.dlg=true;
    this.ctrl.act=act
},
doAct() {
    if(this.ctrl.act=='add') {
        this.add();
    } else {
        this.update();
    }
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat icon="arrow_back" dense @click="ibf.back"></q-btn>
    <q-toolbar-title>{{tags.resume.title}}</q-toolbar-title>
    <q-btn flat icon="add_circle" dense @click="showAct('add')"></q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">
<q-list>
  <q-item v-for="(l,i) in list" clickable @click="showAct('edit',i)">
   <q-item-section>
    <q-item-label>{{l.org}}({{l.type_s}})</q-item-label>
    <q-item-label caption>{{l.start_s}}-{{l.end_s}}</q-item-label>
   </q-item-section>
   <q-item-section>
    <q-item-label>{{l.contrib}}</q-item-label>
    <q-item-label caption>{{l.cmt}}</q-item-label>
   </q-item-section>
  </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="ctrl.dlg" persistent>
  <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{ctrl.tag}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
     <q-input v-model.number="rsInfo.org" :label="tags.resume.org"></q-input>
     <q-select v-model="rsInfo.type" :options="opts.type"
      :label="tags.resume.type" dense map-options emit-value></q-select>

     <div v-if="ctrl.act!='add'">{{rsInfo.start_s}}</div>
     <date-input v-else :close="tags.ok" :label="tags.start" v-model="rsInfo.start_s" max="today"></date-input>

     <date-input :close="tags.ok" :label="tags.end" v-model="rsInfo.end_s" max="today"></date-input>
     <q-input v-model="rsInfo.contrib" :label="tags.resume.contrib"></q-input>
     <q-input v-model="rsInfo.cmt" :label="tags.cmt" type="textarea"></q-input>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn :label="tags.remove" color="indigo" @click="remove(rsInfo.start)" flat></q-btn>
      <q-space></q-space>
      <q-btn :label="tags.ok" color="primary" @click="doAct"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
`
}