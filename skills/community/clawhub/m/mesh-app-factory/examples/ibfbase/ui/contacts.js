export default {
inject:['ibf'],
data() {return {
    list:[], //员工列表
    tags:this.ibf.tags,
    oMap:{}, //办公区映射,officeId=>officeName,zoneId,zoneName
    search:'',
    ctrl:{cur:1, max:0}
}},
created(){
    var req={method:"GET",url:"/api/config/allOffice"};
    request(req, this.ibf.SERVICE_HR).then(resp =>{
        if(resp.code!=RetCode.OK) {
            return;
        }
        this.oMap=resp.data.list;
        this.query(1);
    })
},
methods:{
fmt_lines(rows,cols) {
    var list=[];
    var p,o; //雇员、办公区
    //uid,office,account,worktime,email,name,phone,sex
    for(var row of rows) {
        p={};
        for(var i in cols) {
            p[cols[i]]=row[i];
        }
        p.sex=this.tags.sex[p.sex];
        o=this.oMap[p.office];
        if(o) {
            p.office=o[0]; //offcie,zoneid,zone
            p.zone=o[2];
        } else {
            p.office='';
            p.zone='';
        }
        list.push(p);
    }
    this.list=list;
},
query(pg) {
    this.search='';
    var offset=(parseInt(pg)-1)*this.ibf.N_PAGE;
    var url = "/api/employee/list?offset="+offset+"&num="+this.ibf.N_PAGE;
    request({method:"GET",url:url}, this.ibf.SERVICE_HR).then(resp =>{
        if(resp.code!=RetCode.OK || resp.data.total==0) {
            this.list=[];
            this.ctrl.max=0;
            this.ctrl.cur=1;
            return;
        }
        this.fmt_lines(resp.data.list, resp.data.cols);
        this.ctrl.max=Math.ceil(resp.data.total/this.ibf.N_PAGE);
    })
},
doSearch() {
    if(this.search=='') {
        this.query(1);
        return;
    }
    var url="/api/employee/search?s="+this.search+"&limit="+this.ibf.N_PAGE;
    request({method:"GET",url:url}, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code != RetCode.OK) {
            this.list=[];
            this.ctrl.max=0;
        } else {
            this.fmt_lines(resp.data.pool, resp.data.cols);
            this.ctrl.max=1;
        }
        this.ctrl.cur=1;
    })
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat icon="arrow_back" dense @click="ibf.back"></q-btn>
    <q-toolbar-title>{{tags.contacts.title}}</q-toolbar-title>
  </q-toolbar>
  </q-header>
  <q-footer class="bg-white q-pa-sm">
    <q-input outlined v-model="search" :label="tags.search" dense @keyup.enter="doSearch">
     <template v-slot:append>
      <q-icon v-if="search!==''" name="close" @click="query(1)" class="cursor-pointer"></q-icon>
      <q-icon name="search" @click="doSearch"></q-icon>
     </template>
    </q-input>
  </q-footer>
  <q-page-container>
    <q-page class="q-pa-sm">
<div class="q-pa-sm flex flex-center" v-show="ctrl.max>1">
 <q-pagination v-model="ctrl.cur" color="primary" :max="ctrl.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query"></q-pagination>
</div>
<q-list separator>
 <q-item v-for="p in list">
  <q-item-section>
   <q-item-label>{{p.account}}</q-item-label>
   <q-item-label caption>{{p.name}}({{tags.contacts.level}}:{{p.post}}/{{p.quali}})</q-item-label>
  </q-item-section>
  <q-item-section>
   <q-item-label>{{p.phone}}</q-item-label>
   <q-item-label caption>{{p.email}}</q-item-label>
  </q-item-section>
  <q-item-section side>
   <q-item-label>{{p.office}}</q-item-label>
   <q-item-label caption>{{p.zone}}</q-item-label>
  </q-item-section>
 </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>
`
}