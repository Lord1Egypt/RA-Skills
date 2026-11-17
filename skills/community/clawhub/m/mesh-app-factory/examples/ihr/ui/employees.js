export default {
inject:['service', 'tags', 'ibf'],
data() {return {
    list:[], //员工列表
    search:'',
    ctrl:{cur:1, max:0}
}},
created(){
    this.service.officeList(0).then(() => {
        var pg=this.ibf.getRt('pg', 1);
        this.query(pg);
    });
},
methods:{
fmt_lines(data) {
    var dt=new Date();
    var year=dt.getFullYear();
    var list=[];
    var p; //人才
    var cols=data.cols;
    var rows=data.list;
    //uid,office,quali,post,account,entryAt,email,addr,name,phone
    for(var row of rows) {
        p={};
        for(var i in cols) {
            p[cols[i]]=row[i];
        }
        p.sex=this.tags.sex[p.sex];
        dt.setTime(p.birth*60000);
        p.age=year-dt.getFullYear();
        dt.setTime(p.entryAt*60000);
        p.entryAt=date2str(dt);
        p.office_s=this.service.officeMap[p.office];
        list.push(p);
    }
    this.list=list;
},
query(pg) {
    this.ibf.setRt('pg',pg);
    this.search='';
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var url = "/api/employee/listAll?offset="+offset+"&num="+this.service.N_PAGE;
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
        this.query(this.ibf.getRt('pg', 1));
        return;
    }
    var url="/api/employee/search?s="+this.search+"&limit="+this.service.N_PAGE;
    request({method:"GET",url:url}, this.service.name).then(resp => {
        if(resp.code != RetCode.OK) {
            return;
        }
        this.fmt_lines(resp.data);
        this.ctrl.max=1;
    })
},
detail(id) {
    this.service.goto("/employee?uid="+id)
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
    <q-btn flat icon="arrow_back" dense @click="service.back"></q-btn>
    <q-toolbar-title>{{tags.employee.title}}</q-toolbar-title>
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
<div class="q-pa-sm flex flex-center" v-show="ctrl.max>1">
 <q-pagination v-model="ctrl.cur" color="primary" :max="ctrl.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query"></q-pagination>
</div>
<q-list separator>
 <q-item>
  <q-item-section><q-item-label caption>{{tags.pub.name}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.pub.contact}}</q-item-label></q-item-section>
  <q-item-section side><q-item-label caption>{{tags.pub.ability}}</q-item-label></q-item-section>
 </q-item>
 <q-item v-for="p in list" @click="detail(p.uid)" clickable>
  <q-item-section>
   <q-item-label>{{p.name}} {{p.sex}} {{p.age}}{{tags.age}}</q-item-label>
   <q-item-label caption>{{p.entryAt}}</q-item-label>
  </q-item-section>
  <q-item-section>
   <q-item-label>{{p.phone}}</q-item-label>
   <q-item-label caption>{{p.email}}</q-item-label>
   <q-item-label caption>{{p.office_s}}</q-item-label>
  </q-item-section>
  <q-item-section side>
   <q-item-label caption>{{p.quali}}</q-item-label>
   <q-item-label caption>{{p.post}}</q-item-label>
  </q-item-section>
 </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>
`
}